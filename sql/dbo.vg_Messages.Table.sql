USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_Messages]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_Messages](
	[MessageId] [int] IDENTITY(1,1) NOT NULL,
	[VGProductId] [int] NOT NULL,
	[Message] [varchar](250) NULL,
	[ExpirationDate] [datetime] NULL,
 CONSTRAINT [PK_vg_Messages] PRIMARY KEY CLUSTERED 
(
	[MessageId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
