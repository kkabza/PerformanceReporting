USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_QueueLinks]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_QueueLinks](
	[QueueLinkID] [int] IDENTITY(1,1) NOT NULL,
	[QueueID] [int] NULL,
	[SequenceID] [int] NULL,
 CONSTRAINT [PK_QueueLink_Tbl] PRIMARY KEY CLUSTERED 
(
	[QueueLinkID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
