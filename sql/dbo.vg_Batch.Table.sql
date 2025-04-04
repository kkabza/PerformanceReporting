USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_Batch]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_Batch](
	[BatchID] [int] IDENTITY(1,1) NOT NULL,
	[UserName] [varchar](50) NULL,
	[FileName] [varchar](50) NULL,
	[BatchDesc] [varchar](100) NULL,
	[Status] [int] NULL,
	[Active] [bit] NULL,
	[BatchDate] [datetime] NULL,
	[VGProductID] [int] NULL,
 CONSTRAINT [PK_TDABatch] PRIMARY KEY CLUSTERED 
(
	[BatchID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
